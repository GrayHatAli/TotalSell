using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class CreateReportCommand : BaseCommand
{
    public string Name { get; set; } = null!;
    public string Code { get; set; } = null!;
    public string Type { get; set; } = null!;
    public string? Description { get; set; }
    public Guid CategoryId { get; set; }
    public string? Query { get; set; }
    public string? Parameters { get; set; }
    public string? Filters { get; set; }
    public int? RefreshInterval { get; set; }
    public string? Layout { get; set; }
    public string? Theme { get; set; }
    public bool IsActive { get; set; } = true;
} 