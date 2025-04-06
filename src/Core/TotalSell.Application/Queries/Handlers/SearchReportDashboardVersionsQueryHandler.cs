using AutoMapper;
using MediatR;
using Microsoft.EntityFrameworkCore;
using TotalSell.Application.Common;
using TotalSell.Application.DTOs;
using TotalSell.Application.Queries;
using TotalSell.Domain.Interfaces;

namespace TotalSell.Application.Queries.Handlers;

public class SearchReportDashboardVersionsQueryHandler : IRequestHandler<SearchReportDashboardVersionsQuery, PagedResult<ReportDashboardVersionSummaryDto>>
{
    private readonly IApplicationDbContext _context;
    private readonly IMapper _mapper;

    public SearchReportDashboardVersionsQueryHandler(IApplicationDbContext context, IMapper mapper)
    {
        _context = context;
        _mapper = mapper;
    }

    public async Task<PagedResult<ReportDashboardVersionSummaryDto>> Handle(SearchReportDashboardVersionsQuery request, CancellationToken cancellationToken)
    {
        var query = _context.ReportDashboardVersions.AsQueryable();

        if (!string.IsNullOrWhiteSpace(request.SearchTerm))
        {
            query = query.Where(x => (x.Version ?? "").Contains(request.SearchTerm) || (x.Description ?? "").Contains(request.SearchTerm));
        }

        if (request.DashboardId.HasValue)
        {
            query = query.Where(x => x.DashboardId == request.DashboardId.Value);
        }

        if (!string.IsNullOrWhiteSpace(request.Version))
        {
            query = query.Where(x => x.Version == request.Version);
        }

        if (!string.IsNullOrWhiteSpace(request.Status))
        {
            query = query.Where(x => x.Status == request.Status);
        }

        if (request.IsActive.HasValue)
        {
            query = query.Where(x => x.IsActive == request.IsActive.Value);
        }

        var totalCount = await query.CountAsync(cancellationToken);

        if (!string.IsNullOrWhiteSpace(request.SortBy))
        {
            query = request.SortBy.ToLower() switch
            {
                "version" => request.SortDescending ? query.OrderByDescending(x => x.Version) : query.OrderBy(x => x.Version),
                "status" => request.SortDescending ? query.OrderByDescending(x => x.Status) : query.OrderBy(x => x.Status),
                "createdat" => request.SortDescending ? query.OrderByDescending(x => x.CreatedAt) : query.OrderBy(x => x.CreatedAt),
                _ => query.OrderByDescending(x => x.CreatedAt)
            };
        }
        else
        {
            query = query.OrderByDescending(x => x.CreatedAt);
        }

        var items = await query
            .Skip((request.PageNumber - 1) * request.PageSize)
            .Take(request.PageSize)
            .ToListAsync(cancellationToken);

        return new PagedResult<ReportDashboardVersionSummaryDto>
        {
            Items = _mapper.Map<List<ReportDashboardVersionSummaryDto>>(items),
            TotalCount = totalCount,
            PageNumber = request.PageNumber,
            PageSize = request.PageSize,
            TotalPages = (int)Math.Ceiling(totalCount / (double)request.PageSize)
        };
    }
} 