using TotalSell.Application.Common;

namespace TotalSell.Application.Queries;

public class GetProductQuery : BaseQuery
{
    public Guid ProductId { get; set; }
} 