using MediatR;
using Microsoft.EntityFrameworkCore;
using TotalSell.Application.Common;
using TotalSell.Application.Commands;
using TotalSell.Domain.Entities;

namespace TotalSell.Application.Commands.Handlers;

public class DeactivateReportDashboardVersionCommandHandler : IRequestHandler<DeactivateReportDashboardVersionCommand, Unit>
{
    private readonly IApplicationDbContext _context;

    public DeactivateReportDashboardVersionCommandHandler(IApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<Unit> Handle(DeactivateReportDashboardVersionCommand request, CancellationToken cancellationToken)
    {
        var version = await _context.ReportDashboardVersions
            .FirstOrDefaultAsync(x => x.Id == request.Id, cancellationToken);

        if (version == null)
            throw new KeyNotFoundException($"نسخه داشبورد با شناسه {request.Id} یافت نشد");

        version.Deactivate();
        await _context.SaveChangesAsync(cancellationToken);

        return Unit.Value;
    }
} 