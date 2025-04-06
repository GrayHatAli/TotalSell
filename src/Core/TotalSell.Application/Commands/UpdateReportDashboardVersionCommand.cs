using MediatR;

namespace TotalSell.Application.Commands;

public class UpdateReportDashboardVersionCommand : BaseCommand, IRequest<Unit>
{
    public new Guid Id { get; set; }
    public Guid DashboardId { get; set; }
    public string Version { get; set; } = null!;
    public string? Description { get; set; }
    public string? Layout { get; set; }
    public string? Theme { get; set; }
    public string? Parameters { get; set; }
    public string? Filters { get; set; }
    public int? RefreshInterval { get; set; }
    public bool IsActive { get; set; }
} 