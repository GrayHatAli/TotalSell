using MediatR;
using Microsoft.EntityFrameworkCore;
using TotalSell.Application.Common;
using TotalSell.Application.DTOs;
using TotalSell.Application.Queries;
using AutoMapper;

namespace TotalSell.Application.Queries.Handlers;

public class GetCustomerQueryHandler : IRequestHandler<GetCustomerQuery, CustomerDto>
{
    private readonly IApplicationDbContext _context;
    private readonly IMapper _mapper;

    public GetCustomerQueryHandler(IApplicationDbContext context, IMapper mapper)
    {
        _context = context;
        _mapper = mapper;
    }

    public async Task<CustomerDto> Handle(GetCustomerQuery request, CancellationToken cancellationToken)
    {
        var customer = await _context.Customers
            .FirstOrDefaultAsync(c => c.Id == request.Id, cancellationToken);

        if (customer == null)
            throw new KeyNotFoundException($"Customer with ID {request.Id} not found.");

        return _mapper.Map<CustomerDto>(customer);
    }
} 