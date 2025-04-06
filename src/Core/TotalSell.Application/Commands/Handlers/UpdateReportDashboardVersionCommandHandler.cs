using MediatR;
using Microsoft.EntityFrameworkCore;
using TotalSell.Application.Common;
using TotalSell.Application.Commands;
using TotalSell.Domain.Entities;

namespace TotalSell.Application.Commands.Handlers;

public class UpdateReportDashboardVersionCommandHandler : IRequestHandler<UpdateReportDashboardVersionCommand, Unit>
{
    private readonly IApplicationDbContext _context;

    public UpdateReportDashboardVersionCommandHandler(IApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<Unit> Handle(UpdateReportDashboardVersionCommand request, CancellationToken cancellationToken)
    {
        var version = await _context.ReportDashboardVersions
            .FirstOrDefaultAsync(x => x.Id == request.Id, cancellationToken);

        if (version == null)
            throw new KeyNotFoundException($"نسخه داشبورد با شناسه {request.Id} یافت نشد");

        version.UpdateDetails(
            request.Description ?? "",
            request.Layout ?? "",
            request.Theme ?? "",
            request.Parameters ?? "",
            request.Filters ?? "",
            request.RefreshInterval?.ToString() ?? "");

        await _context.SaveChangesAsync(cancellationToken);

        return Unit.Value;
    }
} 