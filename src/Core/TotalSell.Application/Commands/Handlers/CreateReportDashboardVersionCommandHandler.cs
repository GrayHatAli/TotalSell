using MediatR;
using TotalSell.Application.Common;
using TotalSell.Application.Commands;
using TotalSell.Domain.Entities;

namespace TotalSell.Application.Commands.Handlers;

public class CreateReportDashboardVersionCommandHandler : IRequestHandler<CreateReportDashboardVersionCommand, Guid>
{
    private readonly IApplicationDbContext _context;

    public CreateReportDashboardVersionCommandHandler(IApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<Guid> Handle(CreateReportDashboardVersionCommand request, CancellationToken cancellationToken)
    {
        var version = ReportDashboardVersion.Create(
            request.DashboardId,
            request.Version,
            request.Description,
            request.Layout,
            request.Theme,
            request.Parameters,
            request.Filters,
            request.RefreshInterval);

        _context.ReportDashboardVersions.Add(version);
        await _context.SaveChangesAsync(cancellationToken);

        return version.Id;
    }
} 