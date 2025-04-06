using MediatR;
using TotalSell.Application.Common;
using TotalSell.Application.DTOs;

namespace TotalSell.Application.Queries;

public class GetCustomerQuery : BaseQuery, IRequest<CustomerDto>
{
    public Guid Id { get; set; }
} 