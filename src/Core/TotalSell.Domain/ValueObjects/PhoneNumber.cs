namespace TotalSell.Domain.ValueObjects;

public class PhoneNumber : ValueObject
{
    public string Value { get; }

    private PhoneNumber(string value)
    {
        Value = value;
    }

    public static PhoneNumber Create(string value)
    {
        if (string.IsNullOrWhiteSpace(value))
            throw new ArgumentException("Phone number cannot be empty", nameof(value));

        // Remove any non-digit characters
        var cleanedValue = new string(value.Where(c => char.IsDigit(c)).ToArray());
        
        if (cleanedValue.Length < 10 || cleanedValue.Length > 15)
            throw new ArgumentException("Phone number must be between 10 and 15 digits", nameof(value));

        return new PhoneNumber(cleanedValue);
    }

    protected override IEnumerable<object?> GetEqualityComponents()
    {
        yield return Value;
    }

    public override string ToString()
    {
        return Value;
    }

    public static implicit operator string(PhoneNumber phoneNumber)
    {
        return phoneNumber.Value;
    }
} 