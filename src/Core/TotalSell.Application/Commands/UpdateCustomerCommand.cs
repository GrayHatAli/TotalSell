using MediatR;
using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class UpdateCustomerCommand : BaseCommand, IRequest<Unit>
{
    public new required Guid Id { get; set; }
    public required string Name { get; set; }
    public string? Code { get; set; }
    public string? Description { get; set; }
    public string? Address { get; set; }
    public string? Phone { get; set; }
    public string? Email { get; set; }
    public string? Website { get; set; }
    public string? TaxNumber { get; set; }
    public string? NationalId { get; set; }
    public string? EconomicCode { get; set; }
    public string? PostalCode { get; set; }
    public bool IsActive { get; set; }
} 