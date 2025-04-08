using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using TotalSell.Domain.Entities;

namespace TotalSell.Infrastructure.Persistence.Configurations;

public class InvoiceItemConfiguration : IEntityTypeConfiguration<InvoiceItem>
{
    public void Configure(EntityTypeBuilder<InvoiceItem> builder)
    {
        builder.ToTable("InvoiceItems");
        
        builder.HasKey(i => i.Id);
        
        builder.Property(i => i.Quantity)
            .IsRequired()
            .HasPrecision(18, 2);
            
        builder.Property(i => i.UnitPrice)
            .IsRequired()
            .HasPrecision(18, 2);
            
        builder.Property(i => i.DiscountAmount)
            .HasPrecision(18, 2);
            
        builder.Property(i => i.TaxAmount)
            .HasPrecision(18, 2);
            
        builder.Property(i => i.TotalAmount)
            .HasPrecision(18, 2);
            
        builder.HasOne(i => i.Product)
            .WithMany()
            .HasForeignKey(i => i.ProductId)
            .OnDelete(DeleteBehavior.Restrict);
            
        builder.HasOne(i => i.Invoice)
            .WithMany(i => i.Items)
            .HasForeignKey(i => i.InvoiceId)
            .OnDelete(DeleteBehavior.Cascade);
    }
} 