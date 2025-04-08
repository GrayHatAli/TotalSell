using MediatR;
using Microsoft.EntityFrameworkCore;
using TotalSell.Application.Commands;
using TotalSell.Application.Common.Persistence;

namespace TotalSell.Application.Handlers;

public class DeleteInvoiceCommandHandler : IRequestHandler<DeleteInvoiceCommand, bool>
{
    private readonly ApplicationDbContext _context;

    public DeleteInvoiceCommandHandler(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<bool> Handle(DeleteInvoiceCommand request, CancellationToken cancellationToken)
    {
        var invoice = await _context.Invoices
            .FirstOrDefaultAsync(i => i.Id == request.Id, cancellationToken);

        if (invoice == null)
        {
            throw new ArgumentException("Invoice not found");
        }

        _context.Invoices.Remove(invoice);
        await _context.SaveChangesAsync(cancellationToken);

        return true;
    }
} 