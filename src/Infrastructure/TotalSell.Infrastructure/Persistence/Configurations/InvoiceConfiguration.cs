using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using TotalSell.Domain.Entities;

namespace TotalSell.Infrastructure.Persistence.Configurations;

public class InvoiceConfiguration : IEntityTypeConfiguration<Invoice>
{
    public void Configure(EntityTypeBuilder<Invoice> builder)
    {
        builder.ToTable("Invoices");
        
        builder.HasKey(e => e.Id);
        
        builder.Property(e => e.Number)
            .IsRequired()
            .HasMaxLength(50);
            
        builder.Property(e => e.Date)
            .IsRequired();
            
        builder.Property(e => e.Description)
            .HasMaxLength(500);
            
        builder.Property(e => e.SubTotal)
            .HasPrecision(18, 2);
            
        builder.Property(e => e.TaxAmount)
            .HasPrecision(18, 2);
            
        builder.Property(e => e.DiscountAmount)
            .HasPrecision(18, 2);
            
        builder.Property(e => e.TotalAmount)
            .HasPrecision(18, 2);
            
        builder.Property(e => e.PaymentTerms)
            .HasMaxLength(100);
            
        builder.Property(e => e.DueDate)
            .IsRequired();
            
        builder.Property(e => e.Status)
            .IsRequired()
            .HasMaxLength(50);
            
        builder.HasMany(e => e.Items)
            .WithOne()
            .HasForeignKey("InvoiceId")
            .OnDelete(DeleteBehavior.Cascade);
            
        builder.HasDiscriminator<string>("InvoiceType")
            .HasValue<SalesInvoice>("Sales")
            .HasValue<PurchaseInvoice>("Purchase")
            .HasValue<ProformaInvoice>("Proforma");
    }
} 