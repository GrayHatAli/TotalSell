using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using TotalSell.Domain.Entities;

namespace TotalSell.Infrastructure.Persistence.Configurations;

public class InvoiceConfiguration : IEntityTypeConfiguration<Invoice>
{
    public void Configure(EntityTypeBuilder<Invoice> builder)
    {
        builder.ToTable("Invoices");
        
        builder.HasKey(i => i.Id);
        
        builder.Property(i => i.Number)
            .IsRequired()
            .HasMaxLength(50);
            
        builder.Property(i => i.Date)
            .IsRequired();
            
        builder.Property(i => i.Description)
            .HasMaxLength(500);
            
        builder.Property(i => i.SubTotal)
            .HasPrecision(18, 2);
            
        builder.Property(i => i.TaxAmount)
            .HasPrecision(18, 2);
            
        builder.Property(i => i.DiscountAmount)
            .HasPrecision(18, 2);
            
        builder.Property(i => i.TotalAmount)
            .HasPrecision(18, 2);
            
        builder.Property(i => i.DueDate)
            .IsRequired();
            
        builder.Property(i => i.Status)
            .IsRequired();
            
        builder.Property(i => i.Type)
            .IsRequired();
            
        builder.Property(i => i.CustomerId)
            .IsRequired();
            
        builder.Property(i => i.ReferenceNumber)
            .HasMaxLength(50);
            
        builder.Property(i => i.PaymentMethod)
            .HasMaxLength(50);
            
        builder.HasOne(i => i.Customer)
            .WithMany()
            .HasForeignKey(i => i.CustomerId)
            .OnDelete(DeleteBehavior.Restrict);
            
        builder.HasMany(i => i.Items)
            .WithOne(i => i.Invoice)
            .HasForeignKey(i => i.InvoiceId)
            .OnDelete(DeleteBehavior.Cascade);
    }
} 