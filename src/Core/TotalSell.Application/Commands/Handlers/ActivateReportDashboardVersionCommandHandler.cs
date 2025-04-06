using MediatR;
using Microsoft.EntityFrameworkCore;
using TotalSell.Application.Common;
using TotalSell.Application.Commands;
using TotalSell.Domain.Entities;

namespace TotalSell.Application.Commands.Handlers;

public class ActivateReportDashboardVersionCommandHandler : IRequestHandler<ActivateReportDashboardVersionCommand, Unit>
{
    private readonly IApplicationDbContext _context;

    public ActivateReportDashboardVersionCommandHandler(IApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<Unit> Handle(ActivateReportDashboardVersionCommand request, CancellationToken cancellationToken)
    {
        var version = await _context.ReportDashboardVersions
            .FirstOrDefaultAsync(x => x.Id == request.Id, cancellationToken);

        if (version == null)
            throw new KeyNotFoundException($"نسخه داشبورد با شناسه {request.Id} یافت نشد");

        version.Activate();
        await _context.SaveChangesAsync(cancellationToken);

        return Unit.Value;
    }
} 