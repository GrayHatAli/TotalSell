using MediatR;
using Microsoft.EntityFrameworkCore;
using TotalSell.Application.Common.Persistence;
using TotalSell.Application.DTOs;
using TotalSell.Application.Queries;

namespace TotalSell.Application.Handlers;

public class GetInvoiceQueryHandler : IRequestHandler<GetInvoiceQuery, InvoiceDto>
{
    private readonly ApplicationDbContext _context;

    public GetInvoiceQueryHandler(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<InvoiceDto> Handle(GetInvoiceQuery request, CancellationToken cancellationToken)
    {
        var invoice = await _context.Invoices
            .Include(i => i.Items)
            .Include(i => i.Customer)
            .FirstOrDefaultAsync(i => i.Id == request.Id, cancellationToken);

        if (invoice == null)
        {
            throw new ArgumentException("Invoice not found");
        }

        return new InvoiceDto
        {
            Id = invoice.Id,
            Number = invoice.Number,
            Date = invoice.Date,
            Description = invoice.Description,
            SubTotal = invoice.SubTotal,
            TaxAmount = invoice.TaxAmount,
            DiscountAmount = invoice.DiscountAmount,
            TotalAmount = invoice.TotalAmount,
            DueDate = invoice.DueDate,
            Status = invoice.Status,
            Type = invoice.Type,
            CustomerId = invoice.CustomerId,
            CustomerName = invoice.Customer.Name,
            ReferenceNumber = invoice.ReferenceNumber,
            ReferenceDate = invoice.ReferenceDate,
            PaymentMethod = invoice.PaymentMethod,
            Items = invoice.Items.Select(item => new InvoiceItemDto
            {
                Id = item.Id,
                ProductId = item.ProductId,
                ProductName = item.Product.Name,
                Quantity = item.Quantity,
                UnitPrice = item.UnitPrice,
                DiscountAmount = item.DiscountAmount,
                TaxAmount = item.TaxAmount,
                TotalAmount = item.TotalAmount
            }).ToList()
        };
    }
} 