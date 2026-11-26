namespace AgentWorkflow;

public sealed record UserRequest(string OperationId, string Message);

public sealed record Proposal(string ToolName, bool IsStateChanging, IReadOnlyDictionary<string, object?> Arguments)
{
    public static Proposal Read(string toolName, IReadOnlyDictionary<string, object?>? arguments = null) =>
        new(toolName, false, arguments ?? new Dictionary<string, object?>());

    public static Proposal Write(string toolName, IReadOnlyDictionary<string, object?>? arguments = null) =>
        new(toolName, true, arguments ?? new Dictionary<string, object?>());
}

public sealed record PolicyDecision(bool IsAllowed, string? Reason)
{
    public static PolicyDecision Allow() => new(true, null);
    public static PolicyDecision Block(string reason) => new(false, reason);
}

public sealed record ToolResult(bool Succeeded, string Message);
public sealed record AuditEvent(string OperationId, string EventType, string Detail);
public sealed record WorkflowResult(WorkflowStatus Status, string Message);

public enum WorkflowStatus
{
    Completed,
    Denied,
    Blocked,
    Failed
}

public interface IAgentPlanner
{
    Task<Proposal> PlanAsync(UserRequest request, CancellationToken cancellationToken);
}

public interface IPolicyGate
{
    Task<PolicyDecision> EvaluateAsync(Proposal proposal, CancellationToken cancellationToken);
}

public interface IApprovalService
{
    Task<bool> RequestAsync(Proposal proposal, CancellationToken cancellationToken);
}

public interface IToolGateway
{
    Task<ToolResult> ExecuteAsync(Proposal proposal, string idempotencyKey, CancellationToken cancellationToken);
}

public interface IAuditSink
{
    Task WriteAsync(AuditEvent auditEvent, CancellationToken cancellationToken);
}

public sealed class AgentWorkflowRunner(
    IAgentPlanner planner,
    IPolicyGate policy,
    IApprovalService approvals,
    IToolGateway tools,
    IAuditSink audit)
{
    public async Task<WorkflowResult> RunAsync(
        UserRequest request,
        CancellationToken cancellationToken = default)
    {
        var proposal = await planner.PlanAsync(request, cancellationToken);
        await audit.WriteAsync(
            new AuditEvent(request.OperationId, "proposal.created", proposal.ToolName),
            cancellationToken);

        var decision = await policy.EvaluateAsync(proposal, cancellationToken);
        if (!decision.IsAllowed)
        {
            await audit.WriteAsync(
                new AuditEvent(request.OperationId, "policy.blocked", decision.Reason ?? "Blocked"),
                cancellationToken);
            return new WorkflowResult(WorkflowStatus.Blocked, decision.Reason ?? "Blocked by policy");
        }

        if (proposal.IsStateChanging)
        {
            var approved = await approvals.RequestAsync(proposal, cancellationToken);
            if (!approved)
            {
                await audit.WriteAsync(
                    new AuditEvent(request.OperationId, "approval.denied", proposal.ToolName),
                    cancellationToken);
                return new WorkflowResult(WorkflowStatus.Denied, "The action was not approved");
            }
        }

        var result = await tools.ExecuteAsync(proposal, request.OperationId, cancellationToken);
        await audit.WriteAsync(
            new AuditEvent(
                request.OperationId,
                result.Succeeded ? "tool.completed" : "tool.failed",
                result.Message),
            cancellationToken);

        return result.Succeeded
            ? new WorkflowResult(WorkflowStatus.Completed, result.Message)
            : new WorkflowResult(WorkflowStatus.Failed, result.Message);
    }
}
