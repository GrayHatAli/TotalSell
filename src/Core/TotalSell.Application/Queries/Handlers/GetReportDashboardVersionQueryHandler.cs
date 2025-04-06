using AutoMapper;
using MediatR;
using Microsoft.EntityFrameworkCore;
using TotalSell.Application.Common;
using TotalSell.Application.DTOs;
using TotalSell.Application.Queries;
using TotalSell.Domain.Interfaces;

namespace TotalSell.Application.Queries.Handlers;

public class GetReportDashboardVersionQueryHandler : IRequestHandler<GetReportDashboardVersionQuery, ReportDashboardVersionDto>
{
    private readonly IApplicationDbContext _context;
    private readonly IMapper _mapper;

    public GetReportDashboardVersionQueryHandler(IApplicationDbContext context, IMapper mapper)
    {
        _context = context;
        _mapper = mapper;
    }

    public async Task<ReportDashboardVersionDto> Handle(GetReportDashboardVersionQuery request, CancellationToken cancellationToken)
    {
        var version = await _context.ReportDashboardVersions
            .FirstOrDefaultAsync(x => x.Id == request.VersionId, cancellationToken);

        if (version == null)
            throw new KeyNotFoundException($"نسخه داشبورد با شناسه {request.VersionId} یافت نشد");

        return _mapper.Map<ReportDashboardVersionDto>(version);
    }
} 