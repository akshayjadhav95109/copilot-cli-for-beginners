namespace BookApp.Services;

/// <summary>
/// Validates publication years for books.
/// Valid range: 1000-2100 (historical and near-future publications).
/// </summary>
public static class YearValidator
{
    private const int MinYear = 1000;
    private const int MaxYear = 2100;

    /// <summary>
    /// Determines if a year is valid for publication.
    /// </summary>
    /// <param name="year">The year to validate.</param>
    /// <returns>True if the year is within the valid range, false otherwise.</returns>
    public static bool IsValidYear(int year)
    {
        return year >= MinYear && year <= MaxYear;
    }

    /// <summary>
    /// Gets a descriptive error message for an invalid year.
    /// </summary>
    /// <param name="year">The invalid year.</param>
    /// <returns>A user-friendly error message explaining why the year is invalid.</returns>
    public static string GetErrorMessage(int year)
    {
        if (year < MinYear)
            return $"Year {year} is too early. Please enter a year >= {MinYear}.";
        
        if (year > MaxYear)
            return $"Year {year} is too late. Please enter a year <= {MaxYear}.";
        
        return "Invalid year.";
    }
}
