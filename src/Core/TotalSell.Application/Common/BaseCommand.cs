namespace TotalSell.Application.Common;

public abstract class BaseCommand
{
    public Guid Id { get; set; }
    public string UserId { get; set; } = null!;
} 