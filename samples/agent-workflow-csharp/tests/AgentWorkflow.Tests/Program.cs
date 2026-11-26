using AgentWorkflow;

var tests = new (string Name, Func<Task> Run)[]
{
    ("Read-only proposals execute without approval", ReadOnlyExecutesWithoutApproval),
    ("State-changing proposals require approval", WriteRequiresApproval),
    ("Denied approval blocks tool execution", DeniedApprovalBlocksExecution),
    ("Policy rejection blocks tool execution", PolicyRejectionBlocksExecution),
};

var failures = new List<string>();
foreach (var test in tests)
{
    try
    {
        await test.Run();
        Console.WriteLine($"PASS {test.Name}");
    }
    catch (Exception exception)
    {
        failures.Add($"FAIL {test.Name}: {exception.Message}");
    }
}

foreach (var failure in failures) Console.Error.WriteLine(failure);
return failures.Count == 0 ? 0 : 1;

static async Task ReadOnlyExecutesWithoutApproval()
{
    var fixture = new Fixture(Proposal.Read("SearchCatalog"), approved: false);
    var result = await fixture.Workflow.RunAsync(new UserRequest("op-1", "Find a blue coat"));
    Assert.Equal(WorkflowStatus.Completed, result.Status);
    Assert.Equal(0, fixture.Approvals.RequestCount);
    Assert.Equal(1, fixture.Tools.ExecutionCount);
}

static async Task WriteRequiresApproval()
{
    var fixture = new Fixture(Proposal.Write("AddToCart"), approved: true);
    var result = await fixture.Workflow.RunAsync(new UserRequest("op-2", "Add it to my cart"));
    Assert.Equal(WorkflowStatus.Completed, result.Status);
    Assert.Equal(1, fixture.Approvals.RequestCount);
    Assert.Equal(1, fixture.Tools.ExecutionCount);
}

static async Task DeniedApprovalBlocksExecution()
{
    var fixture = new Fixture(Proposal.Write("PlaceOrder"), approved: false);
    var result = await fixture.Workflow.RunAsync(new UserRequest("op-3", "Buy it"));
    Assert.Equal(WorkflowStatus.Denied, result.Status);
    Assert.Equal(0, fixture.Tools.ExecutionCount);
}

static async Task PolicyRejectionBlocksExecution()
{
    var fixture = new Fixture(Proposal.Read("ExecuteShell"), approved: true, allowed: false);
    var result = await fixture.Workflow.RunAsync(new UserRequest("op-4", "Run a command"));
    Assert.Equal(WorkflowStatus.Blocked, result.Status);
    Assert.Equal(0, fixture.Tools.ExecutionCount);
    Assert.True(fixture.Audit.Events.Any(item => item.EventType == "policy.blocked"));
}

sealed class Fixture
{
    public FakeApproval Approvals { get; }
    public FakeTools Tools { get; } = new();
    public FakeAudit Audit { get; } = new();
    public AgentWorkflowRunner Workflow { get; }

    public Fixture(Proposal proposal, bool approved, bool allowed = true)
    {
        Approvals = new FakeApproval(approved);
        Workflow = new AgentWorkflowRunner(
            new FakePlanner(proposal),
            new FakePolicy(allowed),
            Approvals,
            Tools,
            Audit);
    }
}

sealed class FakePlanner(Proposal proposal) : IAgentPlanner
{
    public Task<Proposal> PlanAsync(UserRequest request, CancellationToken cancellationToken) => Task.FromResult(proposal);
}

sealed class FakePolicy(bool allowed) : IPolicyGate
{
    public Task<PolicyDecision> EvaluateAsync(Proposal proposal, CancellationToken cancellationToken) =>
        Task.FromResult(allowed ? PolicyDecision.Allow() : PolicyDecision.Block("Tool is not allowlisted"));
}

sealed class FakeApproval(bool approved) : IApprovalService
{
    public int RequestCount { get; private set; }
    public Task<bool> RequestAsync(Proposal proposal, CancellationToken cancellationToken)
    {
        RequestCount++;
        return Task.FromResult(approved);
    }
}

sealed class FakeTools : IToolGateway
{
    public int ExecutionCount { get; private set; }
    public Task<ToolResult> ExecuteAsync(Proposal proposal, string idempotencyKey, CancellationToken cancellationToken)
    {
        ExecutionCount++;
        return Task.FromResult(new ToolResult(true, $"Executed {proposal.ToolName}"));
    }
}

sealed class FakeAudit : IAuditSink
{
    public List<AuditEvent> Events { get; } = [];
    public Task WriteAsync(AuditEvent auditEvent, CancellationToken cancellationToken)
    {
        Events.Add(auditEvent);
        return Task.CompletedTask;
    }
}

static class Assert
{
    public static void Equal<T>(T expected, T actual)
    {
        if (!EqualityComparer<T>.Default.Equals(expected, actual))
            throw new InvalidOperationException($"Expected {expected}, got {actual}");
    }

    public static void True(bool value)
    {
        if (!value) throw new InvalidOperationException("Expected true");
    }
}
