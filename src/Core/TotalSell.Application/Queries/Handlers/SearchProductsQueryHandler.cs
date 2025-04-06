using MediatR;
using Microsoft.EntityFrameworkCore;
using TotalSell.Application.Common;
using TotalSell.Application.DTOs;
using TotalSell.Application.Queries;
using AutoMapper;

namespace TotalSell.Application.Queries.Handlers;

public class SearchProductsQueryHandler : IRequestHandler<SearchProductsQuery, IEnumerable<ProductDto>>
{
    private readonly IApplicationDbContext _context;
    private readonly IMapper _mapper;

    public SearchProductsQueryHandler(IApplicationDbContext context, IMapper mapper)
    {
        _context = context;
        _mapper = mapper;
    }

    public async Task<IEnumerable<ProductDto>> Handle(SearchProductsQuery request, CancellationToken cancellationToken)
    {
        var query = _context.Products.AsQueryable();

        if (!string.IsNullOrWhiteSpace(request.Name))
            query = query.Where(p => p.Name.Contains(request.Name));

        if (!string.IsNullOrWhiteSpace(request.Code))
            query = query.Where(p => p.Code.Contains(request.Code));

        if (!string.IsNullOrWhiteSpace(request.Barcode))
            query = query.Where(p => p.Barcode == request.Barcode);

        if (!string.IsNullOrWhiteSpace(request.SKU))
            query = query.Where(p => p.SKU == request.SKU);

        if (!string.IsNullOrWhiteSpace(request.Brand))
            query = query.Where(p => p.Brand == request.Brand);

        if (!string.IsNullOrWhiteSpace(request.Category))
            query = query.Where(p => p.Category == request.Category);

        if (request.IsActive.HasValue)
            query = query.Where(p => p.IsActive == request.IsActive.Value);

        if (request.MinPrice.HasValue)
            query = query.Where(p => p.Price >= request.MinPrice.Value);

        if (request.MaxPrice.HasValue)
            query = query.Where(p => p.Price <= request.MaxPrice.Value);

        if (request.MinStock.HasValue)
            query = query.Where(p => p.StockQuantity >= request.MinStock.Value);

        if (request.Tags.Any())
            query = query.Where(p => p.Tags.Any(t => request.Tags.Contains(t)));

        if (!string.IsNullOrWhiteSpace(request.SortBy))
        {
            query = request.SortBy.ToLower() switch
            {
                "name" => request.SortDescending ? query.OrderByDescending(p => p.Name) : query.OrderBy(p => p.Name),
                "code" => request.SortDescending ? query.OrderByDescending(p => p.Code) : query.OrderBy(p => p.Code),
                "price" => request.SortDescending ? query.OrderByDescending(p => p.Price) : query.OrderBy(p => p.Price),
                "stock" => request.SortDescending ? query.OrderByDescending(p => p.StockQuantity) : query.OrderBy(p => p.StockQuantity),
                _ => query.OrderBy(p => p.Name)
            };
        }

        var products = await query
            .Skip((request.PageNumber - 1) * request.PageSize)
            .Take(request.PageSize)
            .ToListAsync(cancellationToken);

        return _mapper.Map<IEnumerable<ProductDto>>(products);
    }
} 