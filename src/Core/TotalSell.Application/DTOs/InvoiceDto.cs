using TotalSell.Domain.Enums;

namespace TotalSell.Application.DTOs;

public class InvoiceDto
{
    public Guid Id { get; set; }
    public string Number { get; set; } = null!;
    public DateTime Date { get; set; }
    public string? Description { get; set; }
    public decimal SubTotal { get; set; }
    public decimal TaxAmount { get; set; }
    public decimal DiscountAmount { get; set; }
    public decimal TotalAmount { get; set; }
    public DateTime DueDate { get; set; }
    public InvoiceStatus Status { get; set; }
    public InvoiceType Type { get; set; }
    public Guid CustomerId { get; set; }
    public string CustomerName { get; set; } = null!;
    public string? ReferenceNumber { get; set; }
    public DateTime? ReferenceDate { get; set; }
    public string? PaymentMethod { get; set; }
    public List<InvoiceItemDto> Items { get; set; } = new();
}

public class InvoiceItemDto
{
    public Guid Id { get; set; }
    public Guid ProductId { get; set; }
    public string ProductName { get; set; } = null!;
    public decimal Quantity { get; set; }
    public decimal UnitPrice { get; set; }
    public decimal DiscountAmount { get; set; }
    public decimal TaxAmount { get; set; }
    public decimal TotalAmount { get; set; }
} 