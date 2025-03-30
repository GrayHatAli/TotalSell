namespace TotalSell.Domain.Entities;

public class ReportPermission : BaseEntity
{
    public Guid ReportId { get; private set; }
    public Report? Report { get; private set; }
    public string? RoleId { get; private set; }
    public string? RoleName { get; private set; }
    public bool CanView { get; private set; }
    public bool CanExport { get; private set; }
    public bool CanSchedule { get; private set; }
    public bool CanShare { get; private set; }
    public bool IsActive { get; private set; }

    private ReportPermission() { }

    public ReportPermission(
        Guid reportId,
        string roleId,
        string roleName,
        bool canView = false,
        bool canExport = false,
        bool canSchedule = false,
        bool canShare = false)
    {
        ReportId = reportId;
        RoleId = roleId;
        RoleName = roleName;
        CanView = canView;
        CanExport = canExport;
        CanSchedule = canSchedule;
        CanShare = canShare;
        IsActive = true;
    }

    public void UpdatePermissions(
        bool canView,
        bool canExport,
        bool canSchedule,
        bool canShare)
    {
        CanView = canView;
        CanExport = canExport;
        CanSchedule = canSchedule;
        CanShare = canShare;
        UpdatedAt = DateTime.UtcNow;
    }

    public void Deactivate()
    {
        IsActive = false;
        UpdatedAt = DateTime.UtcNow;
    }

    public void Activate()
    {
        IsActive = true;
        UpdatedAt = DateTime.UtcNow;
    }
} 