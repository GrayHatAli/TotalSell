using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using TotalSell.Domain.Entities;

namespace TotalSell.Infrastructure.Persistence.Configurations;

public class ReportDashboardVersionConfiguration : IEntityTypeConfiguration<ReportDashboardVersion>
{
    public void Configure(EntityTypeBuilder<ReportDashboardVersion> builder)
    {
        builder.HasKey(x => x.Id);

        builder.Property(x => x.DashboardId)
            .IsRequired();

        builder.Property(x => x.Version)
            .IsRequired()
            .HasMaxLength(50);

        builder.Property(x => x.Description)
            .HasMaxLength(500);

        builder.Property(x => x.Layout)
            .HasMaxLength(1000);

        builder.Property(x => x.Theme)
            .HasMaxLength(100);

        builder.Property(x => x.Parameters)
            .HasMaxLength(1000);

        builder.Property(x => x.Filters)
            .HasMaxLength(1000);

        builder.Property(x => x.Status)
            .HasMaxLength(50);

        builder.Property(x => x.ApprovedBy)
            .HasMaxLength(100);

        builder.Property(x => x.RejectedBy)
            .HasMaxLength(100);

        builder.Property(x => x.RejectionReason)
            .HasMaxLength(500);

        builder.Property(x => x.CreatedAt)
            .IsRequired();

        builder.Property(x => x.CreatedBy)
            .IsRequired()
            .HasMaxLength(100);

        builder.Property(x => x.UpdatedBy)
            .HasMaxLength(100);
    }
} 