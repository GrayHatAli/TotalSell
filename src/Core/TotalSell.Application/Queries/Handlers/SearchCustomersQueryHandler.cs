using MediatR;
using Microsoft.EntityFrameworkCore;
using TotalSell.Application.Common;
using TotalSell.Application.DTOs;
using TotalSell.Application.Queries;
using AutoMapper;

namespace TotalSell.Application.Queries.Handlers;

public class SearchCustomersQueryHandler : IRequestHandler<SearchCustomersQuery, IEnumerable<CustomerDto>>
{
    private readonly IApplicationDbContext _context;
    private readonly IMapper _mapper;

    public SearchCustomersQueryHandler(IApplicationDbContext context, IMapper mapper)
    {
        _context = context;
        _mapper = mapper;
    }

    public async Task<IEnumerable<CustomerDto>> Handle(SearchCustomersQuery request, CancellationToken cancellationToken)
    {
        var query = _context.Customers.AsQueryable();

        // Apply filters
        if (!string.IsNullOrWhiteSpace(request.Name))
            query = query.Where(c => c.Name.Contains(request.Name));
        
        if (!string.IsNullOrWhiteSpace(request.Code))
            query = query.Where(c => c.Code.Contains(request.Code));
        
        if (!string.IsNullOrWhiteSpace(request.NationalCode))
            query = query.Where(c => c.NationalCode.Contains(request.NationalCode));
        
        if (!string.IsNullOrWhiteSpace(request.EconomicCode))
            query = query.Where(c => c.EconomicCode.Contains(request.EconomicCode));
        
        if (request.IsActive.HasValue)
            query = query.Where(c => c.IsActive == request.IsActive.Value);

        // Apply sorting
        if (!string.IsNullOrWhiteSpace(request.SortBy))
        {
            query = request.SortBy.ToLower() switch
            {
                "name" => request.SortDescending ? query.OrderByDescending(c => c.Name) : query.OrderBy(c => c.Name),
                "code" => request.SortDescending ? query.OrderByDescending(c => c.Code) : query.OrderBy(c => c.Code),
                "createdat" => request.SortDescending ? query.OrderByDescending(c => c.CreatedAt) : query.OrderBy(c => c.CreatedAt),
                _ => query.OrderBy(c => c.Name)
            };
        }
        else
        {
            query = query.OrderBy(c => c.Name);
        }

        // Apply pagination
        query = query.Skip((request.PageNumber - 1) * request.PageSize)
                    .Take(request.PageSize);

        var customers = await query.ToListAsync(cancellationToken);
        return _mapper.Map<IEnumerable<CustomerDto>>(customers);
    }
} 