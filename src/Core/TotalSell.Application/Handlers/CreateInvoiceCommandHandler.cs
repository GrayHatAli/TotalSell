using MediatR;
using Microsoft.EntityFrameworkCore;
using TotalSell.Application.Commands;
using TotalSell.Application.Common.Persistence;
using TotalSell.Domain.Entities;
using TotalSell.Domain.Enums;

namespace TotalSell.Application.Handlers;

public class CreateInvoiceCommandHandler : IRequestHandler<CreateInvoiceCommand, Guid>
{
    private readonly ApplicationDbContext _context;

    public CreateInvoiceCommandHandler(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<Guid> Handle(CreateInvoiceCommand request, CancellationToken cancellationToken)
    {
        // Validate customer exists
        var customer = await _context.Customers
            .FirstOrDefaultAsync(c => c.Id == request.CustomerId, cancellationToken);

        if (customer == null)
        {
            throw new ArgumentException("Customer not found");
        }

        // Create invoice based on type
        Invoice invoice = request.Type switch
        {
            InvoiceType.Sales => SalesInvoice.Create(
                request.Number,
                request.Date,
                request.Description,
                request.DueDate,
                request.Status,
                request.CustomerId,
                customer,
                request.ReferenceNumber,
                request.ReferenceDate,
                request.PaymentMethod),

            InvoiceType.Purchase => PurchaseInvoice.Create(
                request.Number,
                request.Date,
                request.Description,
                request.DueDate,
                request.Status,
                request.CustomerId,
                customer,
                request.SupplierId ?? throw new ArgumentException("SupplierId is required for purchase invoices"),
                request.ReferenceNumber,
                request.ReferenceDate,
                request.PaymentMethod),

            InvoiceType.Proforma => ProformaInvoice.Create(
                request.Number,
                request.Date,
                request.Description,
                request.DueDate,
                request.Status,
                request.CustomerId,
                customer,
                request.ReferenceNumber,
                request.ReferenceDate,
                request.PaymentMethod),

            _ => throw new ArgumentException($"Invalid invoice type: {request.Type}")
        };

        // Add items
        foreach (var item in request.Items)
        {
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

        // Save invoice
        _context.Invoices.Add(invoice);
        await _context.SaveChangesAsync(cancellationToken);

        return invoice.Id;
    }
} 