using MediatR;
using TotalSell.Application.Common;
using TotalSell.Application.DTOs;

namespace TotalSell.Application.Queries;

public class SearchProductsQuery : BaseQuery, IRequest<IEnumerable<ProductDto>>
{
    public string? Name { get; set; }
    public string? Code { get; set; }
    public string? Barcode { get; set; }
    public string? SKU { get; set; }
    public string? Brand { get; set; }
    public string? Category { get; set; }
    public bool? IsActive { get; set; }
    public decimal? MinPrice { get; set; }
    public decimal? MaxPrice { get; set; }
    public decimal? MinStock { get; set; }
    public List<string> Tags { get; set; } = new();
    public int PageNumber { get; set; } = 1;
    public int PageSize { get; set; } = 10;
    public string? SortBy { get; set; }
    public bool SortDescending { get; set; }
} 