using MediatR;
using TotalSell.Application.Common;
using TotalSell.Application.DTOs;
using TotalSell.Domain.Enums;

namespace TotalSell.Application.Queries;

public class SearchInvoicesQuery : BaseQuery, IRequest<IEnumerable<InvoiceDto>>
{
    public string? Number { get; set; }
    public DateTime? FromDate { get; set; }
    public DateTime? ToDate { get; set; }
    public InvoiceStatus? Status { get; set; }
    public decimal? MinTotal { get; set; }
    public decimal? MaxTotal { get; set; }
    public int PageNumber { get; set; } = 1;
    public int PageSize { get; set; } = 10;
    public string? SortBy { get; set; }
    public bool SortDescending { get; set; }
} 