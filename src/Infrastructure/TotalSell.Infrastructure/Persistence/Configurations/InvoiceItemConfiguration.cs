using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using TotalSell.Domain.Entities;

namespace TotalSell.Infrastructure.Persistence.Configurations;

public class InvoiceItemConfiguration : IEntityTypeConfiguration<InvoiceItem>
{
    public void Configure(EntityTypeBuilder<InvoiceItem> builder)
    {
        builder.ToTable("InvoiceItems");
        
        builder.HasKey(e => e.Id);
        
        builder.Property(e => e.InvoiceId)
            .IsRequired();
            
        builder.Property(e => e.ProductId)
            .IsRequired();
            
        builder.Property(e => e.Quantity)
            .HasPrecision(18, 2)
            .IsRequired();
            
        builder.Property(e => e.UnitPrice)
            .HasPrecision(18, 2)
            .IsRequired();
            
        builder.Property(e => e.DiscountAmount)
            .HasPrecision(18, 2);
            
        builder.Property(e => e.TaxAmount)
            .HasPrecision(18, 2);
            
        builder.Property(e => e.TotalAmount)
            .HasPrecision(18, 2);
            
        builder.HasOne(e => e.Product)
            .WithMany()
            .HasForeignKey(e => e.ProductId)
            .OnDelete(DeleteBehavior.Restrict);
            
        builder.HasOne(e => e.Invoice)
            .WithMany(i => i.Items)
            .HasForeignKey(e => e.InvoiceId)
            .OnDelete(DeleteBehavior.Cascade);
    }
} 