using MediatR;
using Microsoft.EntityFrameworkCore;
using TotalSell.Application.Common;
using TotalSell.Application.Commands;
using TotalSell.Domain.Entities;

namespace TotalSell.Application.Commands.Handlers;

public class DeleteReportDashboardVersionCommandHandler : IRequestHandler<DeleteReportDashboardVersionCommand, Unit>
{
    private readonly IApplicationDbContext _context;

    public DeleteReportDashboardVersionCommandHandler(IApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<Unit> Handle(DeleteReportDashboardVersionCommand request, CancellationToken cancellationToken)
    {
        var version = await _context.ReportDashboardVersions
            .FirstOrDefaultAsync(x => x.Id == request.Id, cancellationToken);

        if (version == null)
            throw new KeyNotFoundException($"نسخه داشبورد با شناسه {request.Id} یافت نشد");

        _context.ReportDashboardVersions.Remove(version);
        await _context.SaveChangesAsync(cancellationToken);

        return Unit.Value;
    }
} 