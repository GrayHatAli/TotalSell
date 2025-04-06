using MediatR;
using TotalSell.Application.Common;
using TotalSell.Application.DTOs;

namespace TotalSell.Application.Queries;

public class GetProductQuery : BaseQuery, IRequest<ProductDto>
{
    public Guid Id { get; set; }
} 