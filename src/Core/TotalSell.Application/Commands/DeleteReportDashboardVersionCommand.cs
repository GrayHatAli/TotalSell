using MediatR;
using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class DeleteReportDashboardVersionCommand : IRequest<Unit>
{
    public Guid Id { get; set; }
} 