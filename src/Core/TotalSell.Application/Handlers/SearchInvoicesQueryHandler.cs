using MediatR;
using Microsoft.EntityFrameworkCore;
using TotalSell.Application.Common.Persistence;
using TotalSell.Application.DTOs;
using TotalSell.Application.Queries;

namespace TotalSell.Application.Handlers;

public class SearchInvoicesQueryHandler : IRequestHandler<SearchInvoicesQuery, IEnumerable<InvoiceDto>>
{
    private readonly ApplicationDbContext _context;

    public SearchInvoicesQueryHandler(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<IEnumerable<InvoiceDto>> Handle(SearchInvoicesQuery request, CancellationToken cancellationToken)
    {
        var query = _context.Invoices
            .Include(i => i.Items)
            .Include(i => i.Customer)
            .AsQueryable();

        if (!string.IsNullOrWhiteSpace(request.Number))
        {
            query = query.Where(i => i.Number.Contains(request.Number));
        }

        if (request.FromDate.HasValue)
        {
            query = query.Where(i => i.Date >= request.FromDate.Value);
        }

        if (request.ToDate.HasValue)
        {
            query = query.Where(i => i.Date <= request.ToDate.Value);
        }

        if (request.Status.HasValue)
        {
            query = query.Where(i => i.Status == request.Status.Value);
        }

        if (request.Type.HasValue)
        {
            query = query.Where(i => i.Type == request.Type.Value);
        }

        if (request.CustomerId.HasValue)
        {
            query = query.Where(i => i.CustomerId == request.CustomerId.Value);
        }

        var invoices = await query.ToListAsync(cancellationToken);

        return invoices.Select(invoice => new InvoiceDto
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
        });
    }
} 