namespace TotalSell.Domain.Entities;

public class Tag : BaseEntity
{
    public string Name { get; private set; } = string.Empty;
    public string Code { get; private set; } = string.Empty;
    public string Description { get; private set; } = string.Empty;
    public bool IsActive { get; private set; }

    private Tag() { }

    public Tag(
        string name,
        string code,
        string? description = null)
    {
        Name = name;
        Code = code;
        Description = description ?? string.Empty;
        IsActive = true;
    }

    public void Update(
        string name,
        string code,
        string? description = null)
    {
        Name = name;
        Code = code;
        Description = description ?? string.Empty;
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