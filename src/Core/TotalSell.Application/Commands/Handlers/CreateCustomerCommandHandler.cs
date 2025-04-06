using MediatR;
using TotalSell.Application.Common;
using TotalSell.Application.Commands;
using TotalSell.Domain.Entities;
using AutoMapper;

namespace TotalSell.Application.Commands.Handlers;

public class CreateCustomerCommandHandler : IRequestHandler<CreateCustomerCommand, Guid>
{
    private readonly IApplicationDbContext _context;
    private readonly IMapper _mapper;

    public CreateCustomerCommandHandler(IApplicationDbContext context, IMapper mapper)
    {
        _context = context;
        _mapper = mapper;
    }

    public async Task<Guid> Handle(CreateCustomerCommand request, CancellationToken cancellationToken)
    {
        var customer = _mapper.Map<Customer>(request);
        _context.Customers.Add(customer);
        await _context.SaveChangesAsync(cancellationToken);
        return customer.Id;
    }
} 