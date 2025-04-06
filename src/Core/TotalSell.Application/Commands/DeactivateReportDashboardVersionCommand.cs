using MediatR;
using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class DeactivateReportDashboardVersionCommand : IRequest<Unit>
{
    public Guid Id { get; set; }
} 