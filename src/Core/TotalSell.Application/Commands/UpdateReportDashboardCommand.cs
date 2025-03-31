using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class UpdateReportDashboardCommand : BaseCommand
{
    public new Guid Id { get; set; }
    public string Name { get; set; } = null!;
    public string Code { get; set; } = null!;
    public string? Description { get; set; }
    public string? Layout { get; set; }
    public string? Theme { get; set; }
    public string? Parameters { get; set; }
    public string? Filters { get; set; }
    public int? RefreshInterval { get; set; }
    public bool IsActive { get; set; }
    public IEnumerable<UpdateReportDashboardItemCommand> Items { get; set; } = new List<UpdateReportDashboardItemCommand>();
}

public class UpdateReportDashboardItemCommand
{
    public Guid Id { get; set; }
    public Guid ReportId { get; set; }
    public string Title { get; set; } = null!;
    public string Type { get; set; } = null!;
    public string? Parameters { get; set; }
    public string? Filters { get; set; }
    public string? Layout { get; set; }
    public int Order { get; set; }
    public bool IsActive { get; set; }
} 