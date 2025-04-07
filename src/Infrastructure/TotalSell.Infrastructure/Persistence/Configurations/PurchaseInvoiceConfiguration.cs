using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using TotalSell.Domain.Entities;

namespace TotalSell.Infrastructure.Persistence.Configurations;

public class PurchaseInvoiceConfiguration : IEntityTypeConfiguration<PurchaseInvoice>
{
    public void Configure(EntityTypeBuilder<PurchaseInvoice> builder)
    {
        builder.Property(e => e.SupplierId)
            .IsRequired();
            
        builder.Property(e => e.SupplierInvoiceNumber)
            .HasMaxLength(50);
            
        builder.HasOne(e => e.Supplier)
            .WithMany()
            .HasForeignKey(e => e.SupplierId)
            .OnDelete(DeleteBehavior.Restrict);
    }
} 