using MediatR;
using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class RejectReportDashboardVersionCommand : IRequest<Unit>
{
    public Guid Id { get; set; }
    public string RejectedBy { get; set; } = null!;
    public string RejectionReason { get; set; } = null!;
} 