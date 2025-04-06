using MediatR;

namespace TotalSell.Application.Commands;

public class DeleteReportDashboardVersionCommand : BaseCommand, IRequest<Unit>
{
    public new Guid Id { get; set; }
} 