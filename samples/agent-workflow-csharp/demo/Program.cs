using AgentWorkflow;

var workflow = new AgentWorkflowRunner(
    new ShoppingPlanner(),
    new AllowlistedPolicy(new HashSet<string>(StringComparer.Ordinal)
    {
        "SearchCatalog",
        "AddToCart",
    }),
    new ConsoleApproval(),
    new DemoToolGateway(),
    new ConsoleAudit());

var request = new UserRequest(
    OperationId: $"shopping-{Guid.NewGuid():N}",
    Message: "Add the recommended blue coat to my cart");

var result = await workflow.RunAsync(request);
Console.WriteLine($"RESULT: {result.Status} — {result.Message}");

sealed class ShoppingPlanner : IAgentPlanner
{
    public Task<Proposal> PlanAsync(UserRequest request, CancellationToken cancellationToken)
    {
        // Replace this adapter with Microsoft Agent Framework / Foundry.
        // The model returns a structured proposal; it never calls business APIs directly.
        return Task.FromResult(Proposal.Write(
            "AddToCart",
            new Dictionary<string, object?>
            {
                ["sku"] = "COAT-BLUE-42",
                ["quantity"] = 1,
            }));
    }
}

sealed class AllowlistedPolicy(IReadOnlySet<string> allowedTools) : IPolicyGate
{
    public Task<PolicyDecision> EvaluateAsync(Proposal proposal, CancellationToken cancellationToken) =>
        Task.FromResult(allowedTools.Contains(proposal.ToolName)
            ? PolicyDecision.Allow()
            : PolicyDecision.Block($"Tool '{proposal.ToolName}' is not allowlisted"));
}

sealed class ConsoleApproval : IApprovalService
{
    public Task<bool> RequestAsync(Proposal proposal, CancellationToken cancellationToken)
    {
        Console.WriteLine($"APPROVAL: {proposal.ToolName} {string.Join(", ", proposal.Arguments)}");
        return Task.FromResult(true); // Replace with UI/API approval callback.
    }
}

sealed class DemoToolGateway : IToolGateway
{
    public Task<ToolResult> ExecuteAsync(Proposal proposal, string idempotencyKey, CancellationToken cancellationToken)
    {
        Console.WriteLine($"TOOL: {proposal.ToolName}; idempotency-key={idempotencyKey}");
        return Task.FromResult(new ToolResult(true, "Cart updated"));
    }
}

sealed class ConsoleAudit : IAuditSink
{
    public Task WriteAsync(AuditEvent auditEvent, CancellationToken cancellationToken)
    {
        Console.WriteLine($"AUDIT: {auditEvent.OperationId} {auditEvent.EventType} {auditEvent.Detail}");
        return Task.CompletedTask;
    }
}
