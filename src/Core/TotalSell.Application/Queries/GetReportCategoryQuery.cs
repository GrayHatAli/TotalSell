using TotalSell.Application.Common;

namespace TotalSell.Application.Queries;

public class GetReportCategoryQuery : BaseQuery
{
    public Guid CategoryId { get; set; }
} 