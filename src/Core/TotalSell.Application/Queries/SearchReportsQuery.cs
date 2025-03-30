namespace TotalSell.Application.Queries;

public class SearchReportsQuery : BaseQuery
{
    public string? SearchTerm { get; set; }
    public string? Type { get; set; }
    public string? Status { get; set; }
    public DateTime? FromDate { get; set; }
    public DateTime? ToDate { get; set; }
    public string? CreatedBy { get; set; }
    public string? ApprovedBy { get; set; }
    public bool? IsActive { get; set; }
    public int PageNumber { get; set; } = 1;
    public int PageSize { get; set; } = 10;
    public string? SortBy { get; set; }
    public bool SortDescending { get; set; }
} 