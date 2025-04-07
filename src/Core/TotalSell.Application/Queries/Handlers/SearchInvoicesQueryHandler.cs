using MediatR;
using Microsoft.EntityFrameworkCore;
using TotalSell.Application.Common;
using TotalSell.Application.Queries;
using TotalSell.Application.DTOs;
using AutoMapper;

namespace TotalSell.Application.Queries.Handlers;

public class SearchInvoicesQueryHandler : IRequestHandler<SearchInvoicesQuery, IEnumerable<InvoiceDto>>
{
    private readonly IApplicationDbContext _context;
    private readonly IMapper _mapper;

    public SearchInvoicesQueryHandler(IApplicationDbContext context, IMapper mapper)
    {
        _context = context;
        _mapper = mapper;
    }

    public async Task<IEnumerable<InvoiceDto>> Handle(SearchInvoicesQuery request, CancellationToken cancellationToken)
    {
        var query = _context.Invoices
            .Include(i => i.Items)
            .AsQueryable();

        if (!string.IsNullOrWhiteSpace(request.Number))
            query = query.Where(i => i.Number.Contains(request.Number));

        if (request.FromDate.HasValue)
            query = query.Where(i => i.Date >= request.FromDate.Value);

        if (request.ToDate.HasValue)
            query = query.Where(i => i.Date <= request.ToDate.Value);

        if (request.Status.HasValue)
            query = query.Where(i => i.Status == request.Status.Value);

        if (request.MinTotal.HasValue)
            query = query.Where(i => i.TotalAmount >= request.MinTotal.Value);

        if (request.MaxTotal.HasValue)
            query = query.Where(i => i.TotalAmount <= request.MaxTotal.Value);

        if (!string.IsNullOrWhiteSpace(request.SortBy))
        {
            query = request.SortBy.ToLower() switch
            {
                "number" => request.SortDescending ? query.OrderByDescending(i => i.Number) : query.OrderBy(i => i.Number),
                "date" => request.SortDescending ? query.OrderByDescending(i => i.Date) : query.OrderBy(i => i.Date),
                "totalamount" => request.SortDescending ? query.OrderByDescending(i => i.TotalAmount) : query.OrderBy(i => i.TotalAmount),
                _ => query
            };
        }

        var invoices = await query
            .Skip((request.PageNumber - 1) * request.PageSize)
            .Take(request.PageSize)
            .ToListAsync(cancellationToken);

        return _mapper.Map<IEnumerable<InvoiceDto>>(invoices);
    }
} 