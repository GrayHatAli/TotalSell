namespace TotalSell.Domain.Entities;

public class ReportDashboardPermission : BaseEntity
{
    public Guid DashboardId { get; private set; }
    public ReportDashboard? Dashboard { get; private set; }
    public string? RoleId { get; private set; }
    public string? RoleName { get; private set; }
    public bool CanView { get; private set; }
    public bool CanEdit { get; private set; }
    public bool CanShare { get; private set; }
    public bool IsActive { get; private set; }

    private ReportDashboardPermission() { }

    public ReportDashboardPermission(
        Guid dashboardId,
        string roleId,
        string roleName,
        bool canView = false,
        bool canEdit = false,
        bool canShare = false)
    {
        DashboardId = dashboardId;
        RoleId = roleId;
        RoleName = roleName;
        CanView = canView;
        CanEdit = canEdit;
        CanShare = canShare;
        IsActive = true;
    }

    public void UpdatePermissions(
        bool canView,
        bool canEdit,
        bool canShare)
    {
        CanView = canView;
        CanEdit = canEdit;
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