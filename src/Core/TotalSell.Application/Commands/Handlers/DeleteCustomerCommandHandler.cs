using MediatR;
using Microsoft.EntityFrameworkCore;
using TotalSell.Application.Common;
using TotalSell.Application.Commands;

namespace TotalSell.Application.Commands.Handlers;

public class DeleteCustomerCommandHandler : IRequestHandler<DeleteCustomerCommand, Unit>
{
    private readonly IApplicationDbContext _context;

    public DeleteCustomerCommandHandler(IApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<Unit> Handle(DeleteCustomerCommand request, CancellationToken cancellationToken)
    {
        var customer = await _context.Customers
            .FirstOrDefaultAsync(c => c.Id == request.Id, cancellationToken);

        if (customer == null)
            throw new KeyNotFoundException($"Customer with ID {request.Id} not found.");

        _context.Customers.Remove(customer);
        await _context.SaveChangesAsync(cancellationToken);
        return Unit.Value;
    }
} 