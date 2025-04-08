using MediatR;
using Microsoft.EntityFrameworkCore;
using TotalSell.Application.Commands;
using TotalSell.Application.Common.Persistence;

namespace TotalSell.Application.Handlers;

public class UpdateInvoiceCommandHandler : IRequestHandler<UpdateInvoiceCommand, bool>
{
    private readonly ApplicationDbContext _context;

    public UpdateInvoiceCommandHandler(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<bool> Handle(UpdateInvoiceCommand request, CancellationToken cancellationToken)
    {
        // Get invoice with items
        var invoice = await _context.Invoices
            .Include(i => i.Items)
            .FirstOrDefaultAsync(i => i.Id == request.Id, cancellationToken);

        if (invoice == null)
        {
            throw new ArgumentException("Invoice not found");
        }

        // Validate customer exists
        var customer = await _context.Customers
            .FirstOrDefaultAsync(c => c.Id == request.CustomerId, cancellationToken);

        if (customer == null)
        {
            throw new ArgumentException("Customer not found");
        }

        // Update invoice
        invoice.Update(
            request.Number,
            request.Date,
            request.Description,
            request.DueDate,
            request.Status,
            request.CustomerId,
            customer,
            request.ReferenceNumber,
            request.ReferenceDate,
            request.PaymentMethod);

        // Remove items that are not in the request
        var itemIdsToKeep = request.Items
            .Where(i => i.Id.HasValue)
            .Select(i => i.Id!.Value)
            .ToList();

        var itemsToRemove = invoice.Items
            .ExceptBy(itemIdsToKeep, i => i.Id)
            .ToList();

        foreach (var item in itemsToRemove)
        {
            invoice.RemoveItem(item.Id);
        }

        // Update or add items
        foreach (var item in request.Items)
        {
            if (item.Id.HasValue)
            {
                // Update existing item
                var existingItem = invoice.Items.FirstOrDefault(i => i.Id == item.Id);
                if (existingItem != null)
                {
                    existingItem.Update(
                        item.ProductId,
                        item.Quantity,
                        item.UnitPrice,
                        item.DiscountAmount,
                        item.TaxAmount);
                }
            }
            else
            {
                // Add new item
                var product = await _context.Products
                    .FirstOrDefaultAsync(p => p.Id == item.ProductId, cancellationToken);

                if (product == null)
                {
                    throw new ArgumentException($"Product with ID {item.ProductId} not found");
                }

                invoice.AddItem(
                    item.ProductId,
                    product,
                    item.Quantity,
                    item.UnitPrice,
                    item.DiscountAmount,
                    item.TaxAmount);
            }
        }

        // Save changes
        await _context.SaveChangesAsync(cancellationToken);

        return true;
    }
} 