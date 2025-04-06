using MediatR;
using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class ActivateReportDashboardVersionCommand : IRequest<Unit>
{
    public Guid Id { get; set; }
} 