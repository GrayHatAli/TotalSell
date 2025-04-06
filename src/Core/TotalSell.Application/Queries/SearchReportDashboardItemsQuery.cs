using TotalSell.Application.Common;

namespace TotalSell.Application.Queries;

public class SearchReportDashboardItemsQuery : BaseQuery
{
    public string? SearchTerm { get; set; }
    public Guid? DashboardId { get; set; }
    public string? Type { get; set; }
    public bool? IsActive { get; set; }
    public int PageNumber { get; set; } = 1;
    public int PageSize { get; set; } = 10;
    public string? SortBy { get; set; }
    public bool SortDescending { get; set; }
} 