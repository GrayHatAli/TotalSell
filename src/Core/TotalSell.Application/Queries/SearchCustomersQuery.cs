using MediatR;
using TotalSell.Application.Common;
using TotalSell.Application.DTOs;

namespace TotalSell.Application.Queries;

public class SearchCustomersQuery : BaseQuery, IRequest<IEnumerable<CustomerDto>>
{
    public string? Name { get; set; }
    public string? Code { get; set; }
    public string? NationalCode { get; set; }
    public string? EconomicCode { get; set; }
    public bool? IsActive { get; set; }
    public int PageNumber { get; set; } = 1;
    public int PageSize { get; set; } = 10;
    public string? SortBy { get; set; }
    public bool SortDescending { get; set; }
} 