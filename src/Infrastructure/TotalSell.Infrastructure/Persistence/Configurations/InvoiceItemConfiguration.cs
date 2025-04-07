using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using TotalSell.Domain.Entities;

namespace TotalSell.Infrastructure.Persistence.Configurations;

public class InvoiceItemConfiguration : IEntityTypeConfiguration<InvoiceItem>
{
    public void Configure(EntityTypeBuilder<InvoiceItem> builder)
    {
        builder.HasKey(ii => ii.Id);

        builder.Property(ii => ii.InvoiceId)
            .IsRequired();

        builder.Property(ii => ii.ProductId)
            .IsRequired();

        builder.Property(ii => ii.Quantity)
            .HasPrecision(18, 2)
            .IsRequired();

        builder.Property(ii => ii.UnitPrice)
            .HasPrecision(18, 2)
            .IsRequired();

        builder.Property(ii => ii.DiscountAmount)
            .HasPrecision(18, 2)
            .IsRequired();

        builder.Property(ii => ii.TaxAmount)
            .HasPrecision(18, 2)
            .IsRequired();

        builder.Property(ii => ii.TotalAmount)
            .HasPrecision(18, 2)
            .IsRequired();

        builder.HasOne<Product>()
            .WithMany()
            .HasForeignKey(ii => ii.ProductId)
            .OnDelete(DeleteBehavior.Restrict);
    }
} 