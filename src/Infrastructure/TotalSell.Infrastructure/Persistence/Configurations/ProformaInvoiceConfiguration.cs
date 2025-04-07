using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using TotalSell.Domain.Entities;

namespace TotalSell.Infrastructure.Persistence.Configurations;

public class ProformaInvoiceConfiguration : IEntityTypeConfiguration<ProformaInvoice>
{
    public void Configure(EntityTypeBuilder<ProformaInvoice> builder)
    {
        builder.Property(e => e.CustomerId)
            .IsRequired();
            
        builder.Property(e => e.ReferenceNumber)
            .HasMaxLength(50);
            
        builder.Property(e => e.ReferenceDate);
            
        builder.Property(e => e.PaymentMethod)
            .HasMaxLength(50);
            
        builder.HasOne<Customer>()
            .WithMany()
            .HasForeignKey(e => e.CustomerId)
            .OnDelete(DeleteBehavior.Restrict)
            .HasConstraintName("FK_ProformaInvoices_Customers_CustomerId");
    }
} 