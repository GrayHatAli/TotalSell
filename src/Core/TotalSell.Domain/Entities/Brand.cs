namespace TotalSell.Domain.Entities;

public class Brand : BaseEntity
{
    public string Name { get; private set; } = null!;
    public string Code { get; private set; } = null!;
    public string Description { get; private set; } = null!;
    public string? LogoUrl { get; private set; }
    public bool IsActive { get; private set; }

    private Brand() { }

    public Brand(
        string name,
        string code,
        string description,
        string? logoUrl = null)
    {
        Name = name;
        Code = code;
        Description = description;
        LogoUrl = logoUrl;
        IsActive = true;
    }

    public void Update(
        string name,
        string code,
        string description,
        string? logoUrl = null)
    {
        Name = name;
        Code = code;
        Description = description;
        LogoUrl = logoUrl;
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