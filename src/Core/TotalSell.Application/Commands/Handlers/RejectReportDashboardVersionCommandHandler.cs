using MediatR;
using Microsoft.EntityFrameworkCore;
using TotalSell.Application.Common;
using TotalSell.Application.Commands;
using TotalSell.Domain.Entities;

namespace TotalSell.Application.Commands.Handlers;

public class RejectReportDashboardVersionCommandHandler : IRequestHandler<RejectReportDashboardVersionCommand, Unit>
{
    private readonly IApplicationDbContext _context;

    public RejectReportDashboardVersionCommandHandler(IApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<Unit> Handle(RejectReportDashboardVersionCommand request, CancellationToken cancellationToken)
    {
        var version = await _context.ReportDashboardVersions
            .FirstOrDefaultAsync(x => x.Id == request.Id, cancellationToken);

        if (version == null)
            throw new KeyNotFoundException($"نسخه داشبورد با شناسه {request.Id} یافت نشد");

        version.Reject(request.RejectedBy, request.RejectionReason);
        await _context.SaveChangesAsync(cancellationToken);

        return Unit.Value;
    }
} 