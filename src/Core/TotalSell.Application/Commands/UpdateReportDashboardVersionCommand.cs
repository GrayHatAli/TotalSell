using MediatR;
using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class UpdateReportDashboardVersionCommand : IRequest<Unit>
{
    public Guid Id { get; set; }
    public string? Description { get; set; }
    public string? Layout { get; set; }
    public string? Theme { get; set; }
    public string? Parameters { get; set; }
    public string? Filters { get; set; }
    public int? RefreshInterval { get; set; }
} 